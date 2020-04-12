import json


def lambda_handler(event: dict, context: dict) -> dict:
    """カスタムラベリングのためのプレタスク Lambda 関数
    Args:
        event: dict, required
            SageMaker Ground Truth から 前処理 Lambda へ送られる event は下記のような形。
            詳細は開発者ガイドを参照: https://docs.aws.amazon.com/sagemaker/latest/dg/sms-custom-templates-step3.html 
            {
                "version":"2018-10-16",
                "labelingJobArn":"<your labeling job ARN>",
                "dataObject":{
                    "source-ref":"s3://<your bucket>/<your keys>/awesome.jpg"
                }
            }
        context: object, required
            AWS Lambda Context オブジェクト
            詳細は開発者ガイドを参照: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html
    Returns:
        output: dict
            カスタムラベリングの HTML テンプレートで必要とする内容に応じて変更してください。
            今回は テンプレートで task.input.taskObject を変数として読み込んでいるので、"taskObject" を定義してあります。
            他の変数が必要な場合は、同様に "taskInput" 配下に定義して下さい。
            詳細は開発者ガイドを参照: https://docs.aws.amazon.com/sagemaker/latest/dg/sms-custom-templates-step3.html

            {
                "taskInput":{
                    "taskObject":src_url_http
                },
                "humanAnnotationRequired":"true"
            }
    """

    # 受け取ったイベントを確認
    print("Received event: " + json.dumps(event, indent=2))

    # dataObject 以下にある source もしくは source-ref を受け取る
    source = event['dataObject']['source'] if "source" in event['dataObject'] else None
    source_ref = event['dataObject']['source-ref'] if "source-ref" in event['dataObject'] else None

    # task_object に代入し、アウトプットへ渡す
    task_object = source if source is not None else source_ref
    output = {
        "taskInput": {
            "taskObject": task_object
        },
        "humanAnnotationRequired": "true"
    }

    print(output)

    # source もしくは source-ref のどちらもなかった場合には annotation を失敗させる。
    if task_object is None:
        print(" Failed to pre-process {} !".format(event["labelingJobArn"]))
        output["humanAnnotationRequired"] = "false"

    return output