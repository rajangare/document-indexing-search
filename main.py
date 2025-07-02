from fastapi import FastAPI, Query, UploadFile, File, HTTPException
from pydantic import BaseModel
from starlette.responses import StreamingResponse

from document_indexing_service import DocumentIndexingService
from document_search_service import DocumentSearchService
from elastic_connection import get_elasticsearch_client
from tag_indexing import TagIndexing

app = FastAPI()
elasticInstance = get_elasticsearch_client()
tag_indexing = TagIndexing(elasticInstance)
document_indexing_service = DocumentIndexingService(elasticInstance)
document_search_service = DocumentSearchService(elasticInstance)


# Added this endpoint for testing purposes, no use
@app.get("/search_tags/")
def search_tags(search_semantic_query: str = Query(..., description="Semantic tag search input")):
    tags = tag_indexing.search_tags_by_semantic_string(search_semantic_query)
    return {"tags": tags}


class FileMetadata(BaseModel):
    title: str
    description: str
    tags: list[str]
    access_group: str
    category: str
    link: str
    contact: str

@app.post("/upload/")
async def upload_document(fileMataData: FileMetadata, file: UploadFile = File(...)):
    document_indexing_service.upload_and_index_file(file, fileMataData)

    return {
        "filename": file.filename,
        "content_type": file.content_type
    }




@app.get("/search_document/")
def search_document_metadata(
        semantic_search_query: str = Query(..., description="Semantic search for document metadata")):
    results = document_search_service.search_semantic(semantic_search_query)

    return {"results": results}




@app.get("/download/{file_id}")
async def download_file(file_id: str):
    file_data = document_indexing_service.get_file_by_id(file_id)
    if not file_data:
        raise HTTPException(status_code=404, detail="File not found")
    return StreamingResponse(
        file_data["stream"],
        media_type=file_data["content_type"],
        headers={"Content-Disposition": f"attachment; filename={file_data['filename']}"}
    )


@app.get("/access_groups/")
def get_access_groups():
    # Replace this with your actual logic or data source
    access_groups = [
        "ADMIN",
        "EDITOR",
        "VIEWER",
        "GUEST"
    ]
    return {"access_groups": access_groups}