This repository contains the official [Hydra API](https://siftrics.com/) Python client. The Hydra API is a text recognition service.

# Quickstart

1. Install the package.

```
pip install hydra-api
```

or

```
poetry add hydra-api
```

etc.

1. Create a new data source on [siftrics.com](https://siftrics.com/).
2. Grab an API key from the page of your newly created data source.
3. Create a client, passing your API key into the constructor.
4. Use the client to processes documents, passing in the id of a data source and the filepaths of the documents.

```
import hydra_api

client = hydra_api.Client('xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx')

rows = client.recognize('my_data_source_id', ['invoice.pdf', 'receipt_1.png'])
```

`rows` looks like this:

```
[
  {
    "Error": "",
    "FileIndex": 0,
    "RecognizedText": { ... }
  },
  ...
]
```

`FileIndex` is the index of this file in the original request's "files" array.

`RecognizedText` is a dictionary mapping labels to values. Labels are the titles of the bounding boxes drawn during the creation of the data source. Values are the recognized text inside those bounding boxes.

# Using Base64 Strings Instead of File Paths

There is another function, `client.recognizeBase64(dataSourceId, base64Files, doFaster=False)`, which accepts base64 strings (file contents) instead of file paths. Because it is not trivial to infer MIME type from the contents of a file, you must specify the MIME type associated to each base64 file string: `base64Files` must be a list of `dict` objects containing two fields: `"mimeType"` and ``"base64File"`. Example:

```
    base64Files = [
        {
            'mimeType': 'image/png',
            'base64File': '...',
        },
        {
            'mimeType': 'application/pdf',
            'base64File': '...',
        },
    ]
    rows = client.recognizeBase64('Helm-Test-Againe', base64Files, doFaster=True)
```

# Returning Transformed / Pre-Processed Images

Hydra can transform input documents so they are cropped and aligned with the original image used to create the data source.

The `recognize` and `recognizeBase64` functions have an additional default parameter, `returnTransformedImages`, which defaults to `False`, but if it's set to `True` then Siftrics transforms and returns images so they are aligned with the original image.

Returned images will be available in the "TransformedImages" field of each element of "Rows" in the response:

```
{
  "Rows": [
    {
      "Error": "",
      "FileIndex": 0,
      "RecognizedText": {
        "My Field 1": "text from your document...",
        "My Field 2": "text from your document...",
        ...
      },
      "TransformedImages": [
        {
          "Base64Image": ...,
          "PageNumber": 1
        },
        ...
      ]
    },
    ...
  ]
}
```

# Faster Results

The `recognize` and `recognizeBase64` functions have an additional default parameter, `doFaster`, which defaults to `False`, but if it's set to `True` then Siftrics processes the documents faster at the risk of lower text recognition accuracy. Experimentally, doFaster=true seems not to affect accuracy when all the documents to be processed have been rotated no more than 45 degrees.

# Exporting JPGs instead of PNGs

The `recognize` and `recognizeBase64` functions have additional default parameters, `returnJpgs=False` and `jpgQuality=85`. If `returnJpgs` is set to `True`, then Siftrics returns cropped images in JPG format instead of PNG format. `jpgQuality` must be an integer between 1 and 100 inclusive.

# Official API Documentation

Here is the [official documentation for the Hydra API](https://siftrics.com/docs/hydra.html).

# Apache V2 License

This code is licensed under Apache V2.0. The full text of the license can be found in the "LICENSE" file.
