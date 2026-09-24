resource "aws_redshiftserverless_namespace" "cloudmart_namespace" {
  namespace_name      = "${var.project_name}-namespace"
  admin_username      = var.redshift_admin_username
  admin_user_password  = var.redshift_admin_password
  db_name             = "cloudmart_dw"
  iam_roles           = [aws_iam_role.redshift_role.arn]
}

resource "aws_redshiftserverless_workgroup" "cloudmart_workgroup" {
  workgroup_name = "${var.project_name}-workgroup"
  namespace_name = aws_redshiftserverless_namespace.cloudmart_namespace.namespace_name
  base_capacity  = 8
  publicly_accessible = true
}
