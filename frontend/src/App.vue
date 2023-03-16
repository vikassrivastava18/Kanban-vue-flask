<template>
  <Header></Header>
  
  <Navigation></Navigation>
  <router-view />
 
  <footer>
		Keeping track of daily tasks
	</footer>
</template>

<script>
 import Header from './components/reusable/Header.vue'
 import Navigation from './components/reusable/Navigation.vue'

 export default {
    components: {
    'Header': Header,
    'Navigation': Navigation
  }
}
</script>

<style>
#footer {
  position: fixed;
   bottom: 0;
   width: 100%;
}
</style>

