import { Component, Input } from '@angular/core';
import { LoginUser } from '../../interface/loginuser';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-dashboard',
  imports: [],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent {
  @Input() user?: LoginUser

  constructor(
    private route: ActivatedRoute
  ){}

  getUser() {

  }
}
