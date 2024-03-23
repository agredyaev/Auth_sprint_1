class DataTransformer:
    @staticmethod
    def transform(records):
        transformed_data = []
        for record in records:
            transformed_record = {
                "es_id": record["id"],  # Example transformation
                # Transform other fields as needed
            }
            transformed_data.append(transformed_record)
        return transformed_data
