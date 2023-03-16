<template>
    <div v-if="error">
      <p class="" style="background-color:crimson; color: white;">{{ error.message }}</p>
    </div>
    <div class="container mt-4">
        <h4>Edit List</h4>
        <div class="div" style="max-width: 70vw;">
        <div class="form-group row mt-2">
            <label for="name" class="col-sm-2 col-form-label">Name of List</label>
            <div class="col-sm-10">
            <input type="text" class="form-control" id="name" v-model="listData.name">
            </div>
        </div>
        <br>
        <div class="form-group">
            <button @click="editList" class="btn btn-primary px-4">Edit</button>&nbsp;
            <button type="button" class="btn btn-danger" data-bs-toggle="modal" 
                data-bs-target="#staticBackdrop">Delete
            </button>
        </div>
        
        </div>
    </div> 


<!-- Modal -->
<div class="modal fade" id="staticBackdrop" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="staticBackdropLabel">Are you sure, you want to delete?</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" id="closeModal">Close</button>
        <div class="modal-body">
        <button @click="deleteList()" class="btn btn-danger px-4">Delete</button>
      </div>
      </div>
    </div>
  </div>
</div>
</template>

<script>

import CustomFetch from '../CustomFetch.js'
import { useRoute } from 'vue-router';
export default {
 setup() {

  const route = useRoute();  
  const listData = {
        name: route.query.listName,
        listName: route.query.listName,
      }
  const error = false    
  return {
    listData,
    error
  }  
  },

  data() {
    return {
      error: false
    }
  },

  methods: {
     editList (){
      console.log("list data", this.listData)
      const self = this
      console.log("!@#")  
      CustomFetch(`http://127.0.0.1:8080/api/edit-list/${this.listData.listName}`, {
        method: 'PUT',
        body: JSON.stringify(this.listData),
        headers: {
            'Content-Type': 'application/json',
            'Authorization': localStorage.getItem('Authentication-Token'),
          },
      })
        .then((data) => {
          
          if (data.status == 'fail') {
            self.$router.push({path: '/login'});
          }
          console.log("data", data)
          self.$router.push({path: '/'});
        })
        .catch((err) => {
        //   alert(err.message)
            this.error = error
        })
    },
    deleteList() {
      const listName = this.listData.listName
      console.log("list", listName)
      const self = this
      CustomFetch(`http://127.0.0.1:8080//api/delete-list/${listName}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': localStorage.getItem('Authentication-Token'),
          },
      })
        .then((data) => {
          document.getElementById('closeModal').click();
          self.$router.push({path: '/'});
        })
        .catch((err) => {
        console.log("error", err)
            document.getElementById('closeModal').click();
            this.error = err
            self.$router.push({path: '/login'});
        })
    }
  }
 
}
</script>

