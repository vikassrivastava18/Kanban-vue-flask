<template>
    
    <main class="mt-3 mb-2">

        <div class="d-flex flex-row" >
            
            <div v-for="list in lists"
                :key="list[0]"
                class="d-flex flex-column bd-highlight mb-3 drop-zone" 
                style="margin:20px auto; padding: 10px; border: 1px solid white;"
                    @drop="onDrop($event, list[0])"
                    @dragenter.prevent
                    @dragover.prevent>
                    <h5 class="p-2">
                            {{ list[1] }}
                         <router-link :to="{ path: '/create-card', query: { listId: list[0]}}">
                            <img src="../assets/images/create.png" width="20" alt="create list"
                            >
                         </router-link> &nbsp;
                         <router-link :to="{ path: '/edit-list', query: { listName: list[1]}}"
                         style="float:right">
                                <img src="../assets/images/edit.png" width="23" alt="edit list">
                          </router-link>
                    </h5> 
                    
                <div v-for="card in getCards(list[0])" 
                    class="p-2 bd-highlight drag-el"
                    :key="card.card_id"
                    draggable="true"
                    @dragstart="startDrag($event, card)"> 
                    
                    <details>
                        <summary>
                            {{  card.title }} 
                            <router-link :to="{ path: '/edit-card', 
                            query: { title: card.title, 
                            content: card.content,
                            deadline: card.deadline,
                            completed: card.completed,
                            cardId: card.card_id}}"
                            style="float: right">
                                <img src="../assets/images/edit.png" width="22" alt="edit card">
                            </router-link>
                           
                        </summary>
                        <span>{{ card.content }}</span><br>
                        <span>{{ card.deadline }}</span><br>
                        <span v-if="card.completed">Done</span>
                        <span v-else>Pending</span>
                    </details>
                </div>
                
                <router-link :to="{path: '/list-report', query: {list_id: list[0]}}" 
                  class="btn btn-sm" style="background-color:lightgoldenrodyellow">
                      Report
                </router-link>

                <button class="btn btn-sm mb-1" @click="importCsv(list[0])" style="background-color:lightgreen">Import</button>
            
                
                
              </div>

        </div>    
    
    </main>
  
  
</template>
  
  <script>

  import CustomFetch from '../CustomFetch.js'
  import Header from './reusable/Header.vue'
  import axios from 'axios'
  import { mapActions } from 'vuex'

  export default {
    components: {
    'Header': Header,
  },
    data() {
        return {
            lists_data: [],
            lists: [],
            names:[],
        }
    },
    computed: {
      authenticated() {
        return this.$store.state.authenticated
      }
    },
    methods: {
      ...mapActions([
      'login', // map `this.login()` to `this.$store.dispatch('login')`

      'logout' // map `this.logout()` to `this.$store.dispatch('logout')`
    ]),

     startDrag (event, item){
        event.dataTransfer.dropEffect = 'move'
        event.dataTransfer.effectAllowed = 'move'
        event.dataTransfer.setData('itemID', item.card_id)
        console.log("card_id",item.card_id)
        
      },

      onDrop(event, list_id){
        const itemID = event.dataTransfer.getData('itemID')

        const item = this.lists_data.find((list) => list.card_id == itemID)
        
        item.list_id = list_id

        this.changeServerData(list_id, itemID)
      },

    changeServerData(list_id, card_id) {
        CustomFetch(`http://127.0.0.1:8080/api/change-list`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': localStorage.getItem(
              'Authentication-Token'
            ),
          },
        body: JSON.stringify({
            'list_id': list_id,
            'card_id': card_id
        })
      })
        .then((data) => {
          console.log("data confirm", data)
          
        })
        .catch((err) => {
          alert(err.message)
        })
    },

    getCards(list_id) {
        // return items.value.filter((item) => item.list == list)
        return this.lists_data
        .filter((list) => list.list_id==list_id)
      },

    getListName(list_id) {
        let list = this.lists_data.find((list) => list.list_id == list_id)
        return list.list
    },

    importCsv(list_id) {
      const id = list_id
      axios({
        url: `http://127.0.0.1:8080/api/import-csv/${id}`,
        method: 'POST',
        responseType: 'blob'
        })
        .then((response) => {
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement('a');
          link.href = url;
          const file_name = 'report' + Date.now() + '.csv';
          link.setAttribute('download', file_name);
          document.body.appendChild(link);
          link.click();
        })
      return    

    },
    login() {
      console.log("login")
      this.$store.commit('login');
    },
    logout() {
      console.log("logout")
      this.$store.commit('logout');
    }
      
    },

    mounted() {

        self = this
        CustomFetch(`http://127.0.0.1:8080/api/token-test`, {
        method: 'GET',
        
        headers: {
            'Content-Type': 'application/json',
            'Authorization': localStorage.getItem(
              'Authentication-Token'
            ),
          },
      })
        .then((data) => {
          if (data.status == 'fail') {
            self.$router.push({path: '/login'});
          }
          else {
            this.lists_data = data.slice(1)
            this.lists = data[0]['lists']
            console.log(this.lists)
          }
          
        })
        .catch((err) => {
        //   alert(err.message)
            console.log(err.message, err.status)

        })
    }
  }
  
  </script>
  
  <style>
  
  
  .drop-zone {
    width: 50%;
    margin: 50px auto;
    background-color: rgb(250, 243, 243);
    padding: 10px;
    min-height: 10px;
  }
  
  .drag-el {
    background-color: #d0e5ec;
    /* color: white; */
    padding: 5px;
    margin-bottom: 10px;
  }
  
  .drag-el:nth-child-of-type(1) {
    margin-bottom: 0;
  }
  </style>