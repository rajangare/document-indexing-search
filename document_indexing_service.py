

class DocumentIndexingService:
    global elasticInstance

    def __init__(self, elasticsearch):
        self.elasticsearch = elasticsearch

    def upload_and_index_file(self, file, fileMataData):
        # map the file metadata to documentMetaData
        # Logic to handle file upload and indexing
        # This could include saving the file to a storage location and indexing its content
        # along with the provided metadata into Elasticsearch.
        # Ensure the file is read in binary mode if necessary
        # Example: Read file content and index it
        #file_content = file.read()
        #metadata = self.parse_metadata(fileMataData)

        # Index the file content and metadata
        #self.index_file(file_content, metadata)
        print("File uploaded and indexed successfully.")


    def index_file(self, file, metadata):
        # Logic to index the file content and metadata into Elasticsearch
        pass




