import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { LoginService } from '../../services/login.service';
import { Router } from '@angular/router';
import { StorageService } from 'src/app/services/storage.service';
import { User } from 'src/app/models/user.model';
import { Session } from 'src/app/models/session.model';
import { NavbarComponent } from '../navbar/navbar.component';

@Component({
  selector: 'app-authentication',
  templateUrl: './authentication.component.html',
  styleUrls: ['./authentication.component.scss']
})

export class AuthenticationComponent implements OnInit {

  constructor(private formBuilder: FormBuilder, private loginService: LoginService, private router: Router, private storageService: StorageService) { }

  showModal: boolean;
  registerForm: FormGroup;
  submitted = false;
  userRegisterSuccess = false;

  ngOnInit() : void {
    this.registerForm = this.formBuilder.group({
      name: ['', [Validators.required, Validators.maxLength(16)]],
      surnames: ['', [Validators.required, Validators.maxLength(16)]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      email: ['', [Validators.required, Validators.email]],
    });
  } 

  show() {  this.showModal = true; }  // Show-Hide Modal Check 
  
  hide() { this.showModal = false; }  // Bootstrap Modal Close event

  get f() { return this.registerForm.controls; }  // Convenience getter for easy access to form fields


  /**
  * Register the user inside the database
  *  
  * @param f NgForm 
  * @return void
  */
  onRegisterSubmit(f: NgForm): void {
    this.loginService.insertUser(f.value).subscribe(
      result => {
        this.userRegisterSuccess = !result['success'];
        if (!this.registerForm.invalid && !this.userRegisterSuccess) this.showModal = false;
      }
    );
  }

  /**
   * Sets the user credentials from the API inside sessionStorage
   * 
   * @param f NgForm
   * @return void
   */
  onLoginSubmit(f: NgForm): void {
    this.loginService.login(f.value).subscribe(
      result => { 
        var user = new User(result['name'], result['surnames'], result['role']);
        var session = new Session(result['access_token'], user);
        this.storageService.setCurrentSession(session);
        this.storageService.setLoggedIn(true);
        this.router.navigate(['/perfil']); 
      });
  }


}
