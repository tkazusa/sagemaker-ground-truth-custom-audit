# SageMaker Ground Truth での カスタムテンプレートを活用した検品機能の実装
## 検品までの流れ
- ラベリングジョブを作成し実施
- Amazon Cloud Watch Events で AWS Lambda をトリガーし、検品ジョブを作成する
- 検品ジョブを実施

## ラベリングジョブについて
### 必要なコンポーネント
SageMaker Ground Truth のカスタムテンプレートを使用して Semantic Segmentation を行う場合に必要なコンポーネントは下記。
- HTML テンプレート [segmentation.liquid.html](https://github.com/tkazusa/sagemaker-ground-truth-custom-audit/labelingjob/segmentation.liquid.html)
- プレラベリング Lambda 関数 [pretask.py](https://github.com/tkazusa/sagemaker-ground-truth-custom-audit/labelingjob/pretask.py)
- ポストラベリング Lambda 関数 [posttask.py](https://github.com/tkazusa/sagemaker-ground-truth-custom-audit/labelingjob/posttask.py)
- IAM ロール
    - SageMaker ラベリングジョブ用のロール: `AWSLambdaFullAccess` と `AmazonSageMakerFullAccess` を付与
    - プレラベリング Lambda 関数用のロール: `AWSLambdaBasicExecutionRole` と、 `AmazonS3ReadOnlyAccess`
    - ポストラベリング　Lambda 関数用のロール: `AWSLambdaBasicExecutionRole`


### ラベリングジョブの作成手順
- 各種 IAM ロールの作成
- プレラベリング/ポストラベリング Lambda 関数をランタイム `Python 3.8` で作成
- SageMaker Ground Truth ラベリングジョブを作成
    - タスクのタイプでカスタムを選択
    - テンプレートに `segmentation.liquid.html` の内容をコピー
    - Lambda 関数にそれぞれ、プレラベリング/ポストラベリング Lambda 関数を選択

## 検品ジョブについて
### 必要なコンポーネント
SageMaker Ground Truth のカスタムテンプレートを使用してアノテーション済画像へコメントを行う場合に必要なコンポーネントは下記。
- HTML テンプレート [audit.liquid.html](https://github.com/tkazusa/sagemaker-ground-truth-custom-audit/auditjob/segmentation.liquid.html)
- プレラベリング Lambda 関数 [pretask.py](https://github.com/tkazusa/sagemaker-ground-truth-custom-audit/auditjob/pretask.py)
- ポストラベリング Lambda 関数 [posttask.py](https://github.com/tkazusa/sagemaker-ground-truth-custom-audit/auditingjob/posttask.py)
- IAM ロール
    - SageMaker ラベリングジョブ用のロール: `AWSLambdaFullAccess` と `AmazonSageMakerFullAccess` を付与
    - プレラベリング Lambda 関数用のロール: `AWSLambdaBasicExecutionRole` と、 `AmazonS3ReadOnlyAccess`
    - ポストラベリング　Lambda 関数用のロール: `AWSLambdaBasicExecutionRole`

### 検品ジョブの作成手順
- SageMaker Ground Truth ラベリングジョブを作成
    - マニフェストファイルを作成する際の入力データセットの場所は、ラベリングジョブで画像が出力された S3 パスを指定。
        - `s3://example/annotations/consolidated-annotation/output/`
    - タスクのタイプでカスタムを選択
    - テンプレートに `audit.liquid.html` の内容をコピー
        - TODO: UI へ出力する画像として、元画像とアノテーション後画像を透過してマージ
    - Lambda 関数にそれぞれ、プレラベリング/ポストラベリング Lambda 関数を選択

## TODOs
- 検品ジョブにおいて、UI へ出力する画像として、元画像とアノテーション後画像を透過してマージ 
- 検品ジョブを ラベリングジョブが終わったタイミングで AWS CloudWatch Events をトリガーに AWS Lambda を発火し、Lambda から `CreateLabelingJob` を行う。 