# PM4Moodle frontend: build the Vite/React app, then serve the static files
# with nginx. Two stages keep the runtime image small.

# --- Build stage ---
FROM node:22-alpine AS build
WORKDIR /app

COPY package.json yarn.lock ./
# Install from the committed lockfile so every build resolves the exact same
# dependency versions the project was tested with (npm install would ignore
# yarn.lock and silently pull newer versions).
RUN yarn install --frozen-lockfile

COPY . .

# The API base URL is baked in at build time. It must be reachable from the
# tester's browser, so it points at the backend's published host port.
ARG VITE_API_BASE_URL=http://localhost:5000/api
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
RUN npm run build

# --- Serve stage ---
FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
