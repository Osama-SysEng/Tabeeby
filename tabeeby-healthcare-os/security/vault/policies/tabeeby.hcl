path "secret/tabeeby/*" {
  capabilities = ["read", "list"]
}

path "secret/tabeeby/database/*" {
  capabilities = ["read"]
}

path "secret/tabeeby/encryption/*" {
  capabilities = ["read"]
}
