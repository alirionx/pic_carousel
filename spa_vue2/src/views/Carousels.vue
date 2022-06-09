<template>
  <div class="Carousels">
    <!-- -------------------------------------------------- -->
    <v-card class="ma-6 mt-10 pa-4 elevation-6">
      <v-card-title class="py-2 px-3 text-h7 ">
        <v-row>
          <v-col>Your Carousels</v-col>
          <v-col class="text-right">
            <v-btn 
              small
              fab
              class="purple darken-4 white--text"
              @click="dialogAdd = !dialogAdd"
            >
              <v-icon dark>mdi-plus</v-icon>
            </v-btn>
          </v-col>
          
        </v-row>
      </v-card-title>
      <v-data-table
        :headers="tableHeaders"
        :items="carouselsData"
        :search="search"
      >
        <template v-slot:[`item.imgLen`]="{item}">
          <div v-if="item.images">{{item.images.length}}</div>
          <div v-else>0</div>
        </template>
        <template v-slot:[`item.act`]="{item}">
          <v-btn light icon @click="open_dialog_carousel(carouselsData.indexOf(item))">
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
        </template>
      
      </v-data-table>
    </v-card>

    <!-- -------------------------------------------------- -->
    <v-dialog v-model="dialogAdd" max-width="600px" >
      <form @submit.prevent="submit_add">
        <v-card class="" >
          <v-card-title class="purple darken-3 white--text mb-2">
            Add new Carousel
          </v-card-title>
          <v-card-text class="pt-6" >
            <v-text-field
              v-model="carouselAdd.name"
              label="Carousel Name"
              class="pa-3" 
              required 
            ></v-text-field>
            <v-text-field
              v-model="carouselAdd.description"
              label="Short Description"
              class="pa-3"  
            ></v-text-field>
            <v-select 
              class="pa-3" 
              required 
              label="Switch Mode" 
              v-model="carouselAdd.mode" 
              :items="ddMode"
              >
            </v-select>
            <v-select 
              class="pa-3" 
              required 
              label="State" 
              v-model="carouselAdd.state" 
              :items="ddState"
              >
            </v-select>
            <v-slider
              v-model="carouselAdd.timeout"
              class="pa-3 mt-3" 
              step="1"
              min="1"
              max="30"
              thumb-label
              label="Switch Time" 
              ticks
            ></v-slider>
          </v-card-text>

          <v-card-actions>
            <v-container class="text-center">
              <v-btn
                dark 
                class="purple darken-3 mx-4" 
                min-width="120"
                type="submit"
              >Submit</v-btn>
              <v-btn
                dark 
                class="grey darken-2 mx-4"
                min-width="120"
                type="button"
                @click="close_dialog_add"
              >Close</v-btn>
            </v-container>
          </v-card-actions>
        </v-card>
      </form>
    </v-dialog>

    <!-- --------------------------------------------------------- -->
    <!-- -------------------------------------------------- -->
   
  </div>
</template>


<script>
  // import HelloWorld from '../components/HelloWorld'
  import axios from 'axios'
  import { mapMutations } from 'vuex'

  export default {
    name: 'Carousels',
    data: () => ({
      title: "Carousels",
      title: "Users",
      tableHeaders: [
        { text: 'Name', value: 'name' },
        { text: 'Description', value: 'description' },
        { text: 'Switch Mode', value: 'mode' },
        { text: 'Switch Time', value: 'timeout' },
        { text: 'Images', value: 'imgLen' },
        { text: 'Action', value: 'act' }
      ],
      search: null,
      carouselsData: [],

      dialogAdd: false,
      carouselAdd: {},
      carouselAddTmp: { 
        state:"private",
        mode:"fade",
        timeout: 5,
        // images:[]
      },
      ddMode:[
        {
          text: "Fade",
          value: "fade"
        },
        {
          text: "Slide",
          value: "slide"
        }
      ],
      ddState:[
        {
          text: "Private",
          value: "private"
        },
        {
          text: "Public",
          value: "public"
        },
        {
          text: "Disabled ",
          value: "disabled "
        }
      ],
    }),
    components: {
      
    },
    methods:{
      ...mapMutations([ "set_err", "reset_err" ]),

      //-------------------------------------------
      call_carousels_data(){
        axios.get("/api/carousels", this.$store.getters.create_bearer_auth_header)
        .then((res)=>{
          // console.log(res.data)
          this.carouselsData = res.data
        })
        .catch((err)=>{
          // console.log(err.message)
          this.set_err(err.message)
        })
      },

      //-------------------------------------------
      submit_add(){
        // console.log(this.carouselAdd);
        axios.post(
          "/api/carousels", 
          this.carouselAdd,
          this.$store.getters.create_bearer_auth_header
        )
        .then((res)=>{
          // console.log(res.data._id)
          let newItem = {...this.carouselAdd}
          newItem._id = res.data._id
          this.carouselsData.push(newItem)
        })
        .catch((err)=>{
          this.set_err(err.message)
        })
        .finally(()=>{
          this.close_dialog_add()
        })
      },

      //-------------------------------------------
      close_dialog_add(){
        this.dialogAdd = false;
        this.carouselAdd = {...this.carouselAddTmp}
      },

      //-------------------------------------------
      open_dialog_carousel(idx){
        console.log("open dialog: ", JSON.stringify(this.carouselsData[idx]) )
      },


      //-------------------------------------------


    },
    mounted: function(){
      this.call_carousels_data(),
      this.carouselAdd = {...this.carouselAddTmp}
    }
  }
</script>