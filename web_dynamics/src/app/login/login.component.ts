import { Component } from '@angular/core';
import { Location, NgIf } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { Login } from '../../interface/login';
import { UserService } from '../user.service';
import { LoginUser } from '../../interface/loginuser';

@Component({
  selector: 'app-login',
  imports: [ReactiveFormsModule, NgIf],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  LoginForm = new FormGroup({
    userName : new FormControl('', Validators.required),
    password: new FormControl('', Validators.required)
  })

  user?: any

  constructor(
    private loginService: UserService,
    private location: Location
  ){}

  ngOnInit() {
    this.session()
  }

  session() {
    this.loginService.currentSession()
    .subscribe(
      data => this.user = data
    )
  }

  login() {
    let email = this.LoginForm.value.userName ?? "";
    let password = this.LoginForm.value.password ?? "";

    if (this.LoginForm.valid) {

      const loginDetails: Login = {
        email: email,
        password: password
      }
      this.loginService.loginUser(loginDetails)
      .subscribe(
        data => this.user = data
      )

      this.LoginForm.reset();
    }
  }

  goBack() {
    this.location.back();
  }

}
