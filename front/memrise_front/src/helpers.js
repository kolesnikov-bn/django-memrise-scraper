
export default {
  data: () => ({
    // Snackbar settings.
    snackbar: false,
    position: 'bottom',
    snackColor: '',
    snackErrorColor: 'red lighten-1',
    snackSuccessColor: 'success',
    timeout: 6000,
    message: '',
  }),
  methods: {
    errorHandler (error) {
      /**
       * Создание экземпляра snackbar со статусом ошибка
       * */
      this.snackColor = this.snackErrorColor;
      this.message = error.message;
      this.snackbar = true;
    },
    successHandler (msg) {
      /**
       * Создание экземпляра snackbar со статусом успешно
       * */
      this.snackColor = this.snackSuccessColor;
      this.message = msg;
      this.snackbar = true;
    }
  }
}
