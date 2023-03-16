<template>
<nav v-if="authenticated" class="navbar navbar-expand-lg navbar-light bg-light" style="background-color:crimson">
  <div class="container-fluid">
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item">
          <router-link to="/" class="nav-link">Home</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/create-list" class="nav-link">Create List</router-link>
        </li>

        <li class="nav-item">
          <router-link to="/logout" class="nav-link">Logout</router-link>
        </li>
       
      </ul>
    </div>
  </div>
</nav>

<nav v-else class="navbar navbar-expand-lg navbar-light bg-light" style="background-color:crimson">
  <div class="container-fluid">
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item">
          <router-link to="/login" class="nav-link">Login</router-link>
          <!-- <a class="nav-link active" aria-current="page" href="#">Home</a> -->
        </li>
        <li class="nav-item">
          <router-link to="/register" class="nav-link">Register</router-link>
          <!-- <a class="nav-link" href="#">Features</a> -->
        </li>
        
      </ul>
    </div>
  </div>
</nav>


</template>

<script>
export default {
    computed: {
      authenticated() {
        const self = this
        if (!this.$store.state.authenticated) {
          if (this.$route.path == '/register') {
            self.$router.push({path: '/register'});
          }
          else {
            self.$router.push({path: '/login'});
          }
          
        }
        return this.$store.state.authenticated
      }
    },
}
</script>