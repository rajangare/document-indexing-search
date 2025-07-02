from fastapi import FastAPI, Query, UploadFile, File
from pydantic import BaseModel

from document_indexing_service import DocumentIndexingService
from document_search_service import DocumentSearchService
from elastic_connection import get_elasticsearch_client
from tag_indexing import TagIndexing

app = FastAPI()
elasticInstance = get_elasticsearch_client()
tag_indexing = TagIndexing(elasticInstance)
file_indexing_service = DocumentIndexingService(elasticInstance)
document_search_service = DocumentSearchService(elasticInstance)


# Added this endpoint for testing purposes, no use
@app.get("/search_tags/")
def search_tags(search_semantic_query: str = Query(..., description="Semantic tag search string")):
    tags = tag_indexing.search_tags_by_semantic_string(search_semantic_query)
    return {"tags": tags}


class FileMetadata(BaseModel):
    title: str
    description: str
    tags: list[str]
    access_group: str
    category: str
    link: str

@app.post("/upload/")
async def upload(fileMataData: FileMetadata, file: UploadFile = File(...)):
    file_indexing_service.upload_and_index_file(file, fileMataData)

    return {
        "filename": file.filename,
        "content_type": file.content_type
    }


@app.get("/search_document/")
def search_document_metadata(
        semantic_search_query: str = Query(..., description="Semantic search for document metadata")):
    results = document_search_service.search_semantic(semantic_search_query)

    return {"results": results}
