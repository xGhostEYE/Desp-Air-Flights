<script setup>
defineProps({
  msg: {
    type: String,
    required: true
  }
});
</script>

<template>
    <div>
      <div class="search_box">
        <p class="mb-0">Starting</p>
        <input
          :value="starting"
          @input="event => starting = event.target.value">
          <p class = "mt-5 mb-0">Destination</p>
        <input
          :value="destination"
          @input="event => destination = event.target.value">
          <div>
            <button @click="search()" class="mt-5 btn btn-info">Search</button>
          </div>
      </div> 
    </div>
</template>
<script>
export default {
    data() {
      return {
        starting: '',
        destination: '',
        flight_path: {
          starting: '',
          destination: '',
        },
      }
    },
    methods: {
      search(){
        this.flight_path.starting = this.starting;
        this.flight_path.destination = this.destination;
      }
    },
  };
</script>
<style scoped>
h1 {
  font-weight: 500;
  font-size: 2.6rem;
  top: -10px;
}

h3 {
  font-size: 1.2rem;
}

.greetings h1,
.greetings h3 {
  text-align: center;
}

@media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: left;
  }
}
</style>
