import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { DashboardComponent } from './dashboard/dashboard.component';

export const routes: Routes = [
    {path: 'login', title: "Login Page", component: LoginComponent},
    {path: '', redirectTo: 'login', pathMatch: 'full'},
    {path: 'portal', title: "Portal", component: DashboardComponent}
];
