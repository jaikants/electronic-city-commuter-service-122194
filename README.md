# Project Repository

This is the initial README file for the project.

---

## 🚀 AWS Deployment (Elastic Beanstalk + Secrets/Security)

### 1. Elastic Beanstalk Python/Flask Deployment

- App folder: `backend/`
- Main file: `run.py` (Flask auto-wrapped by WSGI on EB Python environments)
- Use the provided `.ebextensions/flask-env.config` for environment/secret keys.

**Steps:**
1. Zip the contents of the `backend` folder (keeping structure).
2. Deploy via EB CLI:
   ```sh
   eb init -p python-3.11 your-app-name
   eb create your-env-name --envvars FLASK_ENV=production,MONGO_URI=...,JWT_SECRET=...
   ```
   Or set sensitive/secrets in AWS Console → "Configuration" → "Software" → "Environment Properties".

3. The Flask app will be launched via `run.py` as specified in the EB config.

**Managing Secrets:**
- **NEVER** hardcode secrets. Leave the value as `__JWT_SECRET__` in config or reference the variable name.
- Use AWS Elastic Beanstalk environment variables for dev/test.
- For production, store secrets in AWS Secrets Manager, then load them at boot via `.ebextensions`, `secretsmanager_get` scripts, or AWS Parameter Store.

### 2. Docker/ECS Option

- Provided example `Dockerrun.aws.json` (for Dockerized deployment).
- Build and push backend image to Amazon ECR.
- Add secret values/environment keys via ECS task definition/console or with the AWS Secrets integration.

### 3. Security Best Practices for Production

- Do not commit `.env` or real secrets to VCS. Use only placeholders or sample structure.
- Set proper `CORS` origins (not `"*"` for production).
- Use WAF or a load balancer to block unauthorized/unused ports.
- Ensure `JWT_SECRET` and `MONGO_URI` are strong; rotate regularly.
- Use HTTPS everywhere (handled by ELB/ALB).
- Restrict AWS IAM roles assigned to the EB/ECS environment.
- `MONGODB`: restrict access to VPC/private subnet, no open public IPs.
- Regularly scan dependencies for vulnerabilities (`pip-audit`, `dependabot`).

### 4. Updating Secrets

- Via AWS Console: Environment properties.
- Or update via AWS CLI:
  ```
  eb setenv MONGO_URI=your-uri JWT_SECRET=your-secret
  ```

---

For more, see AWS [Deploying Flask on Elastic Beanstalk](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html) and [Secrets Manager Integration](https://docs.aws.amazon.com/secretsmanager/latest/userguide/integrating_cloudformation.html).
