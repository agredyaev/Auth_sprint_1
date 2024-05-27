#!/bin/bash
set -e
set -x

# Extract index name from the JSON file
extract_index_name() {
  local index_file=$1
  basename "$index_file" .json
}

# Create an index from a JSON file
create_index() {
    local index_file=$1
    local index_name=$2

    if curl -I -X HEAD "$ES_DSN/$index_name" | grep -q '200 OK'; then
        echo "Index $index_name already exists. Shipping..."
    else
      echo "Creating index: $index_name"
      curl -X PUT "$ES_DSN/$index_name" -H 'Content-Type: application/json' -d "@$index_file"
      echo "Index $index_name created."
    fi
}

# Load a JSON dump file into an index
load_dump() {
    local index_name=$1
    local dump_file=$2

    echo "Loading dump: $dump_file"
    elasticdump --input "$dump_file" --output "$ES_DSN/$index_name" --type=data
    echo "Dump $dump_file loaded into index: $index_name."
}

# Print usage
usage() {
  echo "Usage: $0 <data_directory> <function_name>"
  echo "Available functions:"
  echo " create_index - Creates an index from a JSON file"
  echo " load_dump - Loads a JSON dump file into an index"
  exit 1
}

# Check if the number of arguments is correct
if [ "$#" -ne 2 ]; then
  usage
fi

# Set the data directory and operation
DATA_DIR=$1
OPERATION=$2

# Define the operations
declare -A operations=(
    ["create_index"]=create_index
    ["load_dump"]=load_dump
)

# Check if the provided operation exists
if [ -z "${operations[$OPERATION]}" ]; then
  echo "Unknown operation: $OPERATION"
  usage
fi

# Execute the operation
for file in ./"$DATA_DIR"/*.json; do
    file_name=$(extract_index_name "$file")
    "${operations[$OPERATION]}" "$file" "$file_name"
done

echo "All tasks completed."