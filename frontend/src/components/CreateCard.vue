<template>

    <div v-if="error">
      <p class="" style="background-color:crimson; color: white;">{{ error.message }}</p>
    </div>

    <div class="container mt-4">
        <h4>Create Card</h4>
        <div class="div" style="max-width: 70vw;">
        <div class="form-group row mt-2">
            <label for="title" class="col-sm-2 col-form-label">Tile of card</label>
            <div class="col-sm-10">
            <input type="text" class="form-control" id="title" v-model="cardData.title">
            </div>
        </div>

        <div class="form-group row mt-2">
            <label for="content" class="col-sm-2 col-form-label">Description of card</label>
            <div class="col-sm-10">
            <input type="text" class="form-control" id="content" v-model="cardData.content">
            </div>
        </div>

        <div class="form-group row mt-2">
            <label for="deadline" class="col-sm-2 col-form-label">Deadline in hours</label>
            <input type="number" id="deadline" min="1" max="100" v-model="cardData.deadline">
        </div>

        <div class="form-group">
            <button @click="createCard" class="btn btn-primary px-4">Create</button>
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

  const cardData = {
        title: '',
        content: '',
        deadline: 0,
        listId: route.query.listId
      }
  const error = false    
  return {
    cardData,
    error
  }  
  },

  data() {
    return {
      error: false
    }
  },

  methods: {
    createCard (){
      console.log("list data", this.cardData)
      const self = this
      console.log("!@#")  
      CustomFetch(`http://127.0.0.1:8080/api/card`, {
        method: 'POST',
        body: JSON.stringify(this.cardData),
        headers: {
            'Content-Type': 'application/json',
            'Authorization': localStorage.getItem('Authentication-Token'),
          },
      })
        .then((data) => {
          console.log("data", data)
          self.$router.push({path: '/'});
        })
        .catch((err) => {
        //   alert(err.message)
        console.log("error", err)
            this.error = err
        })
    }
  }
 
}
</script>

