ALLOWED_ENVS := dev qa demo prod
.PHONY: package changeset deploy s3setup describe events delete

# Require ENV
ifndef ENV
$(error ENV is not set. Please specify a environment name, e.g., 'make <command> ENV=dev')
endif
ifeq ($(filter $(ENV),$(ALLOWED_ENVS)),)
$(error ENV must be one of the following values: $(ALLOWED_ENVS))
endif

package:
	aws cloudformation package --template-file template.yml --s3-bucket ${ENV}-assets-bucket-jenkins-onboarding --s3-prefix ${ENV}-glue-data-catalog --output-template-file packaged-template.yml
changeset:
	aws cloudformation deploy --template-file packaged-template.yml --stack-name ${ENV}-glue-data-catalog --parameter-overrides Stage=${ENV} ProjectName=glue-data-catalog --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM --no-execute-changeset
deploy:
	aws cloudformation package --template-file template.yml --s3-bucket ${ENV}-assets-bucket-jenkins-onboarding --s3-prefix ${ENV}-glue-data-catalog --output-template-file packaged-template.yml
	aws cloudformation deploy --template-file packaged-template.yml --stack-name ${ENV}-glue-data-catalog --parameter-overrides Stage=${ENV} ProjectName=glue-data-catalog --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM
s3setup:
	aws cloudformation describe-stacks \
	--stack-name ${ENV}-glue-data-catalog \
	--query 'Stacks[0].Outputs[?OutputKey==`s3Bucket`].OutputValue' \
	--output text \
	| xargs -I {} aws s3 cp local/customer.csv s3://{}/input/customers/customer.csv
describe:
	aws cloudformation describe-stacks --stack-name ${ENV}-glue-data-catalog --color on
events:
	aws cloudformation describe-stack-events --stack-name ${ENV}-glue-data-catalog
delete:
	aws cloudformation describe-stacks \
	--stack-name ${ENV}-glue-data-catalog \
	--query 'Stacks[0].Outputs[?OutputKey==`s3Bucket`].OutputValue' \
	--output text \
	| xargs -I {} aws s3 rm s3://{} --recursive
	aws cloudformation delete-stack --stack-name ${ENV}-glue-data-catalog
