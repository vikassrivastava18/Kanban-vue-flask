import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import './assets/main.css'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.js'

import { createStore } from 'vuex'
import CustomFetch from './customFetch'

function check_auth() {
    const token = localStorage.getItem('Authentication-Token')
    if (token) {
        return true
    //     CustomFetch(`http://127.0.0.1:8080/api/token-test`, {
    //     method: 'GET',
        
    //     headers: {
    //         'Content-Type': 'application/json',
    //         'Authorization': localStorage.getItem(
    //           'Authentication-Token'
    //         ),
    //       },
    //   })
    //     .then((data) => {
    //       if (data.status == 'fail') {
    //         return false
    //       }
    //       else {
    //         return true
    //       }
          
    //     })
    //     .catch((err) => {
    //     //   alert(err.message)
    //         console.log(err.message, err.status)
    //         return false
    //     })
    }
    return false
}

const store = createStore({
    state () {
      return {
        authenticated: check_auth()
      }
    },
    mutations: {
      login (state) {
        state.authenticated = true
      },
      logout (state) {
        state.authenticated = false
      }

    },
    actions: {
        login () {
            // do something with the token
            context.commit('login')
        },
        logout () {
            context.commit('logout')
        }
    }
  })


createApp(App)
    .use(router)
    .use(store)
    .mount('#app')


