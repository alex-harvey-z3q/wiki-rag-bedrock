variable "db_username" {
  type        = string
  default     = "wikirdb"
  description = "Username for the PostgreSQL database used by the RAG application."
}

variable "ingest_schedule" {
  type        = string
  default     = "rate(6 hours)"
  description = "EventBridge schedule expression controlling how often the Wikipedia ingestion task runs."
}

variable "github_repo" {
  type        = string
  default     = "alex-harvey-z3q/wiki-rag"
  description = "GitHub repo in owner/repo format"
}
