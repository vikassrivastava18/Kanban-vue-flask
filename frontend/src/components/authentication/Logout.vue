<template>
    <div class="container">
      <div v-if="error">
        <p class="" style="background-color:crimson; color: white;">Wrong credentials, please try again!</p>
      </div>
      <h4>Logged out</h4>
      <router-link to="/login">Login</router-link>
    </div>

</template>

<script>

export default {
 mounted() {
    // CustomFetch(`http://127.0.0.1:8080/api/logout`, {
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
    //         self.$router.push({path: '/login'});
    //       }
    //       else {
    //         localStorage.removeItem('Authentication-Token')
    //         return
    //       }
         
          
    //     })
    //     .catch((err) => {
    //     //   alert(err.message)
    //         console.log(err.message, err.status)

    //     })
    localStorage.removeItem('Authentication-Token')
    this.$store.commit('logout');
    return
 }
 
}
</script>

