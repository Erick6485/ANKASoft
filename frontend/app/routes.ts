import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  index("routes/login.tsx"),
  route("dashboard", "routes/dashboard.tsx"),
  route("centro-control", "routes/centro-control.tsx"),
  route("inventario", "routes/inventario.tsx"),
  route("ventas", "routes/ventas.tsx"),
  route("patrones", "routes/patrones.tsx"),
  route("analytics", "routes/analytics.tsx"),
  route("kpis", "routes/kpis.tsx"),
  route("alertas", "routes/alertas.tsx"),
  route("reportes", "routes/reportes.tsx"),
  route("configuracion", "routes/configuracion.tsx"),
] satisfies RouteConfig;
