import "vue-router";

declare module "vue-router" {
  interface RouteMeta {
    isAdmin?: boolean;
    requiresAuth: boolean;
  }
}

import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import Home from "@/views/Home.vue";
import Search from "@/views/Search.vue";
import QA from "@/views/QA.vue";
import Upload from "@/views/Upload.vue";
import { AuthClient } from "@/main";
import Store from "@/store/index";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/:id",
    name: "QA",
    component: QA,
  },
  {
    path: "/search",
    name: "Search",
    component: Search,
  },
  {
    path: "/upload",
    name: "Upload",
    component: Upload,
    meta: {
      requiresAuth: true,
    },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to) => {
  try {
    if (to.query.code && to.query.state) {
      const { appState } = await AuthClient.handleRedirectCallback();
      router.push(
        appState && appState.targetUrl
          ? appState.targetUrl
          : window.location.pathname
      );
    }
  } catch (error) {
    console.log(error);
  } finally {
    Store.state.auth.isAuthenticated = await AuthClient.isAuthenticated();
    Store.state.auth.user = await AuthClient.getUser();
  }
  // const isAuthenticated = await AuthClient.isAuthenticated();
  if (to.meta.requiresAuth && !Store.state.auth.isAuthenticated) {
    return router.push("/");
  }
});

export default router;
