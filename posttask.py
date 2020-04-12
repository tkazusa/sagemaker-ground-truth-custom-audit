
import json
import sys

def lambda_handler(event: dict, context: object) -> dict:
    """ カスタムラベリングのためのポストタスク Lambda 関数
    Args:
        event: dict, required
            SageMaker Ground Truth から 後処理 Lambda へ送られる event は下記のような形。
            詳細は開発者ガイドを参照: https://docs.aws.amazon.com/sagemaker/latest/dg/sms-custom-templates-step3.html 
            
            {
                "version": "2018-10-16",
                "labelingJobArn": <labelingJobArn>,
                "labelCategories": [<string>],  # If you created labeling job using aws console, labelCategories will be null
                "labelAttributeName": <string>,
                "roleArn" : "string",
                "payload": {
                    "s3Uri": <string>
                }
                "outputConfig":"s3://<consolidated_output configured for labeling job>"
            }

            payload.s3Uri は下記。

            [
                {
                    "datasetObjectId": <string>,
                    "dataObject": {
                        "s3Uri": <string>,
                        "content": <string>
                    },
                    "annotations": [{
                        "workerId": <string>,
                        "annotationData": {
                            "content": <string>,
                            "s3Uri": <string>
                            }
                        }
                    ]
                }
            ]

        context: object, required
            AWS Lambda Context オブジェク
            詳細は開発者ガイドを参照: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html
    Returns:
        consolidated_output: list
        統合されたアノテーション結果。
        詳細は開発者ガイドを参照: 
            [
                {
                    "datasetObjectId": <string>,
                    "consolidatedAnnotation": {
                        "content": {
                            "<labelattributename>": {
                                # ... label content
                            }
                        }
                    }
                }
            ]
    """

    # 受け取ったイベントを確認
    print("Received event: " + json.dumps(event, indent=2))

    # S3 URI から
    parsed_url = urlparse(event['payload']['s3Uri'])

    s3 = boto3.client('s3')
    textFile = s3.get_object(Bucket=parsed_url.netloc, Key=parsed_url.path[1:])
    filecont = textFile['Body'].read()
    annotations = json.loads(filecont)

    for dataset in annotations:
        for annotation in dataset['annotations']:
            new_annotation = json.loads(
                annotation['annotationData']['content'])

            label ={
                'datasetObjectId': dataset['datasetObjectId'],
                'consolidatedAnnotation': {
                    'content': {
                        event['labelAttributeName']: {
                            'workerId': annotation['workerId'],
                            'result': new_annotation,
                            'labeledContent': dataset['dataObject']
                        }
                    }
                }
            }
            
            consolidated_labels.append(label)

    # Response の確認
    print("Response: " + json.dumps(consolidated_labels))

    return consolidated_labels