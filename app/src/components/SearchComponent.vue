<script setup>
defineProps({
  airports: {
    type: Array,
    required: true
  }
});
let validStarting = true;
let validDestination = true;

const inputClasses = function(isValid) {
  return [
    'mb-3',
    'alert',
    isValid? 'alert-light':'',
    isValid? '':'alert-danger'
  ];
};



</script>
<template>
    <div class="align-items-center justify-content-center">

        <label for="starting" class="form-label">Starting</label>
        <input class="form-control" list="startingList" name="starting" 
                id="starting" v-model="starting" 
                type="text" />
        <span :class="{'invisible':this.validStarting}" class="form-text text-danger">Enter valid airport</span>
        <datalist id="startingList">
          <option v-for="airport in this.airports">{{airport}}</option>
        </datalist>
      
      
        <label for="destination" class="form-label">Destination</label>
        <input class="form-control" list="destinationList" name="destination" 
                id="destination" v-model="destination" />
        <span :class="{'invisible':this.validStarting}" class="form-text text-danger">Enter valid airport</span>
        <datalist id="destinationList">
          <option v-for="airport in this.airports">{{airport}}</option>
        </datalist>
        
        <div>
          <button :class="{'disabled': !this.validEntries()}" @click="search()" class="mt-5 btn btn-primary">Search</button>
        </div>
    </div>
</template>
<script>
export default {
    data() {
      return {
        starting: '',
        destination: '',
      }
    },
    methods: {
      search(){
        this.validStarting = this.airports.includes(this.starting);
        if (this.validStarting)
          this.$emit('getFlights', this.starting, this.destination);
      },
      validEntries() {        
        return this.airports.includes(this.starting) && this.airports.includes(this.destination);
      },
      validateinput(value, validString) {
        if (value.length) {
          for (let airport of this.airports) {
            this[validString] = airport.toLowerCase().startsWith(value.toLowerCase());
            if (this[validString]) break;
          }
          this.validEntries();
        }
      }
      
    },
    watch: {
      starting(value) {
        this.validateinput(value, "validStarting");
      },
      destination(value) {
        this.validateinput(value, "validDestination");
      },
    },
  };
</script>
