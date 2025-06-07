
#!/bin/bash
set -e

# === Аргументы (можно передавать) ===
SERVER_CN="${1:-fastapi.internal}"
SERVER_SAN="${2:-IP:127.0.0.1}"
CLIENT_CN="${3:-nginx-client}"
FASTAPI_HOST="${4:-138.124.124.211}"
FASTAPI_PORT="${5:-8000}"

# === Структура директорий ===
OUTDIR="mtls_bundle"
CERTDIR="$OUTDIR/certs"
mkdir -p "$CERTDIR"

echo "🔧 Создание CA..."
openssl genrsa -out "$CERTDIR/ca.key" 4096
openssl req -x509 -new -nodes -key "$CERTDIR/ca.key" -sha256 -days 1825 \
  -out "$CERTDIR/ca.crt" -subj "/CN=MyCustomCA"

# === SAN-конфигурация для сервера ===
cat > "$CERTDIR/server-ext.cnf" <<EOF
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, keyEncipherment
subjectAltName = ${SERVER_SAN}
EOF

echo "🔐 Сертификат сервера: CN=${SERVER_CN}, SAN=${SERVER_SAN}..."
openssl genrsa -out "$CERTDIR/server.key" 2048
openssl req -new -key "$CERTDIR/server.key" -out "$CERTDIR/server.csr" -subj "/CN=${SERVER_CN}"
openssl x509 -req -in "$CERTDIR/server.csr" -CA "$CERTDIR/ca.crt" -CAkey "$CERTDIR/ca.key" -CAcreateserial \
  -out "$CERTDIR/server.crt" -days 825 -sha256 -extfile "$CERTDIR/server-ext.cnf"

echo "🔐 Сертификат клиента: CN=${CLIENT_CN}..."
openssl genrsa -out "$CERTDIR/client.key" 2048
openssl req -new -key "$CERTDIR/client.key" -out "$CERTDIR/client.csr" -subj "/CN=${CLIENT_CN}"
openssl x509 -req -in "$CERTDIR/client.csr" -CA "$CERTDIR/ca.crt" -CAkey "$CERTDIR/ca.key" -CAcreateserial \
  -out "$CERTDIR/client.crt" -days 825 -sha256

echo "📝 Генерация nginx.conf..."

cat > "$OUTDIR/nginx.conf" <<EOF
server {
    listen 443 ssl;
    server_name ${SERVER_CN};

    ssl_certificate     /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;

    location /api/ {
        proxy_pass https://${FASTAPI_HOST}:${FASTAPI_PORT};

        proxy_ssl_certificate     /etc/nginx/ssl/client.crt;
        proxy_ssl_certificate_key /etc/nginx/ssl/client.key;
        proxy_ssl_trusted_certificate /etc/nginx/ssl/ca.crt;

        proxy_ssl_verify on;
        proxy_ssl_verify_depth 2;
        proxy_ssl_session_reuse off;
    }
}
EOF

echo "📦 Упаковка завершена. Файлы готовы в директории: $OUTDIR"

echo "🔁 Пример копирования на сервер:"
echo "scp -r $OUTDIR user@server:/path/to/nginx"


# Пример
# bash generate-mtls-bundle.sh fastapi.internal "IP:138.124.124.211" nginx-client 138.124.124.211 8000