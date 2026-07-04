# ---------- مرحلهٔ ۱: ساخت React ----------
FROM node:22-alpine AS build

WORKDIR /build
COPY package*.json ./
RUN npm ci

COPY . .
# در استقرار، API از همان دامنه زیر /api سرو می‌شود (پروکسی nginx) → بدون CORS
ENV VITE_API_URL=/api
RUN npm run build

# ---------- مرحلهٔ ۲: سرو با nginx ----------
FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /build/dist /usr/share/nginx/html

EXPOSE 80
