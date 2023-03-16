<template>

      <div v-if="error">
        <p class="" style="background-color:crimson; color: white;">{{ message }}</p>
      </div>
      <div class="container">
        <h4>Register</h4>
        <div class="div" style="max-width: 70vw;">
        <div class="form-group row mt-2">
          <label for="username" class="col-sm-2 col-form-label">username</label>
          <div class="col-sm-10">
            <input type="text" class="form-control" id="username" v-model="registerData.username"
            placeholder="Username">
          </div>
        </div>
        <div class="form-group row mt-2">
          <label for="staticEmail" class="col-sm-2 col-form-label">Email</label>
          <div class="col-sm-10">
            <input type="text" class="form-control" id="staticEmail" v-model="registerData.email"
            placeholder="Email">
          </div>
        </div>
        <div class="form-group row">
          <label for="inputPassword" class="col-sm-2 col-form-label">Password</label>
          <div class="col-sm-10">
            <input type="password" class="form-control" id="inputPassword" placeholder="Password" v-model="registerData.password">
          </div>
        </div>
        <div class="form-group">
          <button @click="register" class="btn btn-primary px-4">Submit</button>
        </div>
        </div>
      </div>
        
  
  </template>
  
  <script>
  import CustomFetch from '../../CustomFetch.js'
  export default {
   setup() {
    const registerData = {
          username: '',
          email: '',
          password: '',
        }
  
    return {
      registerData
    }  
    },

  data() {
    return {
      error: false,
      message: ''
    }
  },
  
    methods: {
       register (){
        const self = this;
        console.log(this.registerData)
        CustomFetch(`http://127.0.0.1:8080/api/register`, {
          method: 'POST',
          body: JSON.stringify(this.registerData),
          headers: {
            'Content-Type': 'application/json',
          },
        })
          .then((data) => {
            if(data.status == 'fail') {
              this.error = true
              this.message = data.error
              return
            }
            console.log("data!", data)
            self.$router.push({path: '/login'});
            
          })
          .catch((err) => {
            alert(err.message)
          })
      }
    }
   
  }
  </script>
  
  