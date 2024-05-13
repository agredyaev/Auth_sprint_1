#!/bin/bash
set -e
set -x

create_index() {
    local index_file=$1
    local index_name=$(basename "$index_file" .json)

    if curl -I -X HEAD "$ES_DSN/$index_name" | grep -q '200 OK'; then
        echo "Index $index_name already exists. Shipping..."
    else
      echo "Creating index: $index_name"
      curl -X PUT "$ES_DSN/$index_name" -H 'Content-Type: application/json' -d "@$index_file"
      echo "Index $index_name created."
    fi
}

for index_file in ./indices/*.json; do
    create_index "$index_file"
done

echo "All indexes have been created."