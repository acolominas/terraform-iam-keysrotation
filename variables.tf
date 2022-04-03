variable "days" {
  type        = string
  description = "Number of days to rotate keys"
  default     = "90"
}

variable "users" {
  type        = string
  description = "Coma-separated string with IAM users to rotate keys"
}
