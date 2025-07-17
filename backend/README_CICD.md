# Electronic City Commuter Service Backend – AWS CI/CD and Deployment

## CI/CD Flow

- **AWS CodePipeline** triggers on main branch changes, using CodeBuild.
- **CodeBuild**:
  - Installs Python requirements and runs backend tests.
  - Fetches secrets (Mongo URI, JWT secret) from AWS Secrets Manager, makes them available at runtime.
  - Zips backend/ for deploy.
  - Deploys artifact to Elastic Beanstalk (or ECS if Dockerized).

## Secrets Management

- Store in AWS Secrets Manager as a **single secret** with all Flask env keys (JSON: `{ "MONGO_URI": "...", "JWT_SECRET": "..." }`).
- Use `buildspec.yml` to fetch secrets at build time or entrypoint script.
- *Never* commit actual secrets to git.

## Manual Steps (One-Time Setup)

1. Create EB application/environment (or ECS Cluster/Service) in AWS.
2. Create S3 bucket for artifacts.
3. Store required secrets in AWS Secrets Manager.
4. Assign pipeline/service roles with permission for S3, EB, Secrets Manager.
5. Connect repository via CodeStar or source action.
6. Update pipeline template placeholders with your resource names.

## Artifacts

- Backend: Deployable zip (`backend-deploy.zip`).
- Mobile: Android `.apk`/`.aab`, iOS `.ipa`.

## Mobile App CI/CD (Flutter)

- Use `mobile_frontend/buildspec.yml` for Android/iOS CI builds.
- Artifacts output to `build_artifacts`.
- For signing/production distribution, securely provide signing certificates/keys using encrypted variables or AWS Secrets (never commit).

## References

- [AWS Flask + Elastic Beanstalk Guide](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html)
- [AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)
- [AWS CodeBuild Spec](https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html)
- [Flutter Build via CI](https://docs.flutter.dev/deployment/cd)

## Security Best Practices

- Use Secrets Manager or SSM Parameter Store for all credentials.
- Only use placeholder/secrets in `Dockerrun.aws.json`.
- Run test and lint in CodeBuild.
- For production deploy, set `FLASK_ENV=production`.
