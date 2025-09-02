import os
import torch
from sentence_transformers import util
from typing import Optional, List
from aimlpy.model.document_record import PDFDocument
from aimlpy.util.pdfutil import extract_pdf_metadata 
from sentence_transformers import SentenceTransformer
from aimlpy.repo.datasource import DataSource
from fastapi import UploadFile, Query
from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from sklearn.metrics.pairwise import cosine_similarity

UPLOAD_DIR = "uploads" 
model = SentenceTransformer("all-MiniLM-L6-v2")

class DocumentService:
    def __init__(self, session: Optional[Session] = None):
        self.session: Session = session or DataSource().get_session()

    async def add_document(self, title: str, file: UploadFile) -> Optional[PDFDocument]:
        try:
            if not title.strip():
                raise ValueError("Title cannot be empty.")
            if file.content_type != "application/pdf":
                raise ValueError("Only PDF files are allowed.")

            contents = await file.read()

            os.makedirs(UPLOAD_DIR, exist_ok=True)
            file_location = os.path.join(UPLOAD_DIR, file.filename)
            with open(file_location, "wb") as f:
                f.write(contents)

            metadata = extract_pdf_metadata(file_location)
            doc_title = metadata.get("title") or title
            author = metadata.get("author") or "Unknown"
            summary = metadata.get("summary")
            keywords = metadata.get("keywords")
            created_at = metadata.get("created_at")

            text_for_embedding = metadata.get("full_text") or summary or doc_title
            if not text_for_embedding:
                raise ValueError("Document has no readable content for embedding.")

            embedding = model.encode(text_for_embedding).tolist()

            #plagiarism check
            existing_docs = self.session.query(PDFDocument).all()
            existing_embeddings = [doc.embedding for doc in existing_docs if doc.embedding]
            existing_authors = [doc.author for doc in existing_docs]

            if existing_embeddings:
                similarity_scores = cosine_similarity([embedding], existing_embeddings)[0]
                for i, score in enumerate(similarity_scores):
                    if score > 0.85 and existing_authors[i] != author:
                        print(f"Plagiarism detected: Similarity {score:.2f} with author {existing_authors[i]}")
                        return None  #abort upload

            #save document
            new_doc = PDFDocument(
                title=doc_title,
                author=author,
                keywords=keywords,
                summary=summary,
                created_at=created_at,
                filename=file.filename,
                embedding=embedding,
            )

            self.session.add(new_doc)
            self.session.commit()
            self.session.refresh(new_doc)

            return new_doc

        except Exception as e:
            self.session.rollback()
            raise Exception(f"Failed to add document: {str(e)}")
        finally:
            self.session.close()

    async def list_documents(
        self,
        author: Optional[str],
        keyword: Optional[str],
        date_from: Optional[str],
        date_to: Optional[str],
    ) -> List[PDFDocument]:
        filters = []

        if author:
            filters.append(PDFDocument.author.ilike(f"%{author}%"))

        if keyword:
            filters.append(PDFDocument.keywords.any(keyword))  

        if date_from:
            try:
                date_from_parsed = datetime.strptime(date_from, "%Y-%m-%d")
                filters.append(PDFDocument.created_at >= date_from_parsed)
            except ValueError:
                pass

        if date_to:
            try:
                date_to_parsed = datetime.strptime(date_to, "%Y-%m-%d")
                filters.append(PDFDocument.created_at <= date_to_parsed)
            except ValueError:
                pass

        query = select(PDFDocument)
        if filters:
            query = query.where(and_(*filters))

        result = self.session.execute(query)
        return result.scalars().all()
    
    def search_documents(self, query: str) -> List[PDFDocument]:
        if not query.strip():
            return []

        stmt = select(PDFDocument).where(PDFDocument.embedding.isnot(None))
        result = self.session.execute(stmt)
        all_documents = result.scalars().all()

        if not all_documents:
            return []

        query_embedding = model.encode(query, convert_to_tensor=True)

        doc_embeddings = torch.tensor([doc.embedding for doc in all_documents])
        cos_scores = util.pytorch_cos_sim(query_embedding, doc_embeddings)[0]

        # hybrid scoring
        scored_docs = []
        for doc, semantic_score in zip(all_documents, cos_scores):
            semantic_score = semantic_score.item()

            keyword_match = any([
                query.lower() in (doc.title or "").lower(),
                query.lower() in (doc.author or "").lower(),
                query.lower() in (doc.summary or "").lower(),
                any(query.lower() in kw.lower() for kw in (doc.keywords or []))
            ])
            keyword_score = 1.0 if keyword_match else 0.0
            final_score = 0.4 * keyword_score + 0.6 * semantic_score

            scored_docs.append((doc, final_score))

        scored_docs.sort(key=lambda x: x[1], reverse=True)
        top_documents = [doc for doc, _ in scored_docs[:1]]  # return top 1

        return top_documents
