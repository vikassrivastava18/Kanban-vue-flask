import { createRouter, createWebHistory } from 'vue-router'
import Home from './components/Home.vue'
import Login from './components/authentication/Login.vue'
import Logout from './components/authentication/Logout.vue'
import CreateList from './components/CreateList.vue'
import EditList from './components/EditList.vue'
import CreateCard from './components/CreateCard.vue'
import EditCard from './components/EditCard.vue'
import Report from './components/Report.vue'
import Register from './components/authentication/Register.vue'


export default createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: Home,
    },
    {
      path: '/login',
      component: Login,
      },
      {
        path: '/register',
        component: Register,
        },
      {
        path: '/logout',
        component: Logout,
        },  
    {
        path: '/create-list',
        component: CreateList,
    },
    {
      path: '/edit-list',
      component: EditList,
  },
    {
        path: '/create-card',
        component: CreateCard,
    },
    {
        path: '/edit-card',
        component: EditCard,
    },
    {
      path: '/list-report',
      component: Report,
  },
  ]
})