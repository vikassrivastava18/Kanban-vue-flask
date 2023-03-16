<template>

    <div v-if="error">
      <p class="" style="background-color:crimson; color: white;">Wrong credentials, please try again!</p>
    </div>
    <div class="container">
      <h4>Login</h4>
    <div class="div" style="max-width: 70vw;">
      <div class="form-group row mt-2">
        <label for="staticEmail" class="col-sm-2 col-form-label">Email</label>
        <div class="col-sm-10">
          <input type="text" class="form-control" id="staticEmail" 
          v-model="loginData.email" placeholder="youremail@gmail.com">
        </div>
      </div>
      <div class="form-group row">
        <label for="inputPassword" class="col-sm-2 col-form-label">Password</label>
        <div class="col-sm-10">
          <input type="password" class="form-control" id="inputPassword" placeholder="Password" v-model="loginData.password">
        </div>
      </div>
      <div class="form-group">
        <button @click="login" class="btn btn-primary px-4">Submit</button>
      </div>
    </div>
    </div>
    

</template>

<script>
import CustomFetch from '../../CustomFetch.js'
export default {
 setup() {
  const loginData = {
        email: '',
        password: '',
      }
  return {
    loginData,
  }  
  },

  data() {
    return {
      error: false
    }
  },

  methods: {
     login (){
      const self = this;
      console.log('data', this.loginData)
      CustomFetch(`http://127.0.0.1:8080/api/login`, {
        method: 'POST',
        body: JSON.stringify(this.loginData),
        headers: {
          'Content-Type': 'application/json',
        },
      })
        .then((data) => {
          console.log("data!", data)
          if (data.status == 'fail') {
            console.log("wrong credentials")
            this.error = true
            return
          }
          localStorage.setItem(
            'Authentication-Token',
            data['auth_token']
          )
          this.$store.commit('login');
          self.$router.push({path: '/'});
        })
        .catch((err) => {
          alert(err.message)
        })
    }
  }
 
}
</script>

