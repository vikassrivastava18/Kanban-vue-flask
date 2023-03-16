<template>
    
    <div v-if="error">
      <p class="" style="background-color:crimson; color: white;">{{ error.message }}</p>
    </div>

    <div class="container mt-4 mb-5">
        <h4>Edit Card</h4>
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
            <input type="text" class="form-control" id="content" v-model="cardData.content" 
             >
            </div>
        </div>

        <div class="form-group row mt-2">
             <p>Last deadline - {{  cardData.deadline }}</p>
            <label for="deadline" class="col-sm-2 col-form-label">Deadline in hours</label>
            <input type="number" id="deadline" min="1" max="100" v-model="cardData.deadline">

        </div>

        <div class="form-check mt-2 p-2">
            <label class="form-check-label" for="completed">
                Completed
            </label>
            <input class="form-check-input" type="checkbox" value="" id="completed"
            v-model="cardData.completed" checked="cardData.completed">
        </div>

        <div class="form-group mt-2">
            <button @click="editCard()" class="btn btn-primary px-4 mx-2">Update</button>
            <!-- Button trigger modal -->
            <button type="button" class="btn btn-danger" data-bs-toggle="modal" 
            data-bs-target="#staticBackdrop">
              Delete
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
        <button @click="deleteCard()" class="btn btn-danger px-4">Delete</button>
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

  const cardData = {
        title: route.query.title,
        content: route.query.content,
        completed: route.query.completed,
        cardId: route.query.cardId,
        deadline: route.query.deadline
      }
  const error = false    
  return {
    route,
    cardData,
    error,
  }  
  },

  data() {
    return {
      error: false
    }
  },

  methods: {
    editCard (){
      console.log("card completed", this.cardData.completed)
      console.log("card id", this.cardData.cardId)
      const cardId = this.cardData.cardId
      const self = this
      CustomFetch(`http://127.0.0.1:8080/api/card/${cardId}`, {
        method: 'PUT',
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
        console.log("error", err)
            this.error = err
            self.$router.push({path: '/login'});
        })
    },
    deleteCard() {
      const cardId = this.cardData.cardId
      console.log("card", cardId)
      const self = this
      CustomFetch(`http://127.0.0.1:8080/api/card/${cardId}`, {
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
            this.error = err
            self.$router.push({path: '/login'});
        })
    }
  },
  mounted() {

  }
}
</script>

