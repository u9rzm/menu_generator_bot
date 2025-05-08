FROM nginx:latest

# Установка curl для health check
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Добавим wait-for-it
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Копируем конфиг
COPY test.conf /etc/nginx/conf.d/default.conf

# Создаем скрипт для проверки здоровья API
RUN echo '#!/bin/sh\n\
while ! curl -s http://api:${API_PORT}/api/health > /dev/null; do\n\
  echo "Waiting for API..."\n\
  sleep 1\n\
done\n\
echo "API is ready!"\n\
nginx -g "daemon off;"' > /docker-entrypoint.sh && \
chmod +x /docker-entrypoint.sh

# Стартовая команда
CMD ["/docker-entrypoint.sh"]
