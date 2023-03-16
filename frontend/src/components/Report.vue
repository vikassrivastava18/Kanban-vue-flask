<template>
    <div class="container p-5">
        <Bar
        v-if="loaded"
        id="my-chart-id"
        :options="chartOptions"
        :data="chartData"
        :style="myStyles"
        />
    </div>
  </template>
  
  <script>
  import { Bar } from 'vue-chartjs'
  import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
  import CustomFetch from '../CustomFetch.js'

  ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)
  import { useRoute } from 'vue-router';
//   const route = useRoute();

  export default {

  setup() {
  
    const route = useRoute();
    const listId = route.query.list_id;
    return {
        listId
    }
    },

    name: 'BarChart',
    components: { Bar },
    
    data() {
      return {
        loaded: false,
        chartData: {
          labels: [ 'Finished In Time', 'Late Completion', 'Pending' , 'Backlog'],
          datasets: [ 
            { 
            data: [1,3,4,6],
            backgroundColor: 'lightblue',
            label: '123',
            }
         ],
        },
        chartOptions: {
          responsive: true
        }
      }
    },
    computed: {
      myStyles () {
        return {
            width: '50px',
            position: 'relative'
        }
     }
    },

 mounted() {
    this.loaded = false
    const self = this
    console.log("!@#")  
    CustomFetch(`http://127.0.0.1:8080/api/list-report/${this.listId}`, {
      method: 'GET',
      headers: {
          'Content-Type': 'application/json',
          'Authorization': localStorage.getItem('Authentication-Token'),
        },
    })
      .then((data) => {
        if (data.status == 'fail') {
          self.$router.push({path: '/login'});
        }  
        console.log('label', this.chartData.datasets[0]['label'])
        // console.log(this.chartData.datasets[0]['data'], 'data')
        this.chartData.datasets[0]['data'] = data.slice(0,4)
        this.chartData.datasets[0]['label'] = data[4]
        console.log('label', this.chartData.datasets[0]['label'])
        this.loaded = true
        return
        
      })
      .catch((err) => {
      //   alert(err.message)
          console.log("error", err)
      })
  }
}
  </script>
  