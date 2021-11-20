import { createRouter, createWebHistory } from "vue-router"
import HelloWorld from '../components/HelloWorld.vue'
import About from '../components/About.vue'
import NotFound from "../components/NotFound.vue"



const routes = [
    { path: "/", component: HelloWorld },
    { path: "/about", component: About },
    { path: '/:pathMatch(.*)*', name: 'not-found', component: NotFound }

]

export default createRouter({ history: createWebHistory("/web/"), routes })