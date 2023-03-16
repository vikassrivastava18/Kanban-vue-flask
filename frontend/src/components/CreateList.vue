<template>
    <div v-if="error">
      <p class="" style="background-color:crimson; color: white;">{{ error.message }}</p>
    </div>
    <div class="container mt-4">
        <h4>Create List</h4>
        <div class="div" style="max-width: 70vw;">
        <div class="form-group row mt-2">
            <label for="name" class="col-sm-2 col-form-label">Name of List</label>
            <div class="col-sm-10">
            <input type="text" class="form-control" id="name" v-model="listData.name">
            </div>
        </div>
        
        <div class="form-group">
            <button @click="createList" class="btn btn-primary px-4">Create</button>
        </div>
        </div>
    </div> 

</template>

<script>
import CustomFetch from '../CustomFetch.js'
export default {
 setup() {
  const listData = {
        name: '',
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
     createList (){
      console.log("list data", this.listData)
      const self = this
      console.log("!@#")  
      CustomFetch(`http://127.0.0.1:8080/api/create-list`, {
        method: 'POST',
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
    }
  }
 
}
</script>

