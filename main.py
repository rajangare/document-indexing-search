from fastapi import FastAPI, Query, UploadFile, File, HTTPException, Form, Depends
from starlette.responses import StreamingResponse

from document_indexing_service import DocumentIndexingService, DOCUMENT_DESC_INDEX, DOCUMENT_NAME_INDEX, \
    DOCUMENT_TAG_INDEX
from document_search_service import DocumentSearchService
from elastic_connection import get_elasticsearch_client
from file_metadata import FileMetadata
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


# Dependency to extract metadata fields from Form
def get_metadata(
    title: str = Form(...),
    description: str = Form(...),
    tags: list[str] = Form(...),  # Expecting a JSON string
    access_group: str = Form(...),
    category: str = Form(...),
    link: str = Form(...),
    contact: str = Form(...)
) -> FileMetadata:
    return FileMetadata(
        title=title,
        description=description,
        tags=tags,
        access_group=access_group,
        category=category,
        link=link,
        contact=contact
    )

document_indexing_service.create_index(DOCUMENT_DESC_INDEX)  # Ensure the index exists at startup
document_indexing_service.create_index(DOCUMENT_NAME_INDEX)  # Ensure the index exists at startup
document_indexing_service.create_index(DOCUMENT_TAG_INDEX)  # Ensure the index exists at startup

@app.post("/upload/")
async def upload_document(fileMataData: FileMetadata = Depends(get_metadata), fileUpload: UploadFile = File(None)):
    print("File Metadata:", fileMataData)
    return {"file_reference":document_indexing_service.upload_and_index_file(fileUpload, fileMataData)}


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

@app.get("/filepath/{file_id}")
def get_filepath_by_fileid(file_id: str):
    file_path = document_indexing_service.get_file_by_id(file_id)
    if file_path is not None:
        return {"file_path": file_path}
    raise HTTPException(status_code=404, detail="File not found")


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

