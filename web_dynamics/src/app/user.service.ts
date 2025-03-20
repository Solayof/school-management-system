import { Injectable } from '@angular/core';
import { Observable, tap, catchError, of } from 'rxjs';
import { Login } from '../interface/login';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  constructor(
    private http: HttpClient
  ) { }

  httpOption = {
    headers: new HttpHeaders({'Content-Type': 'application/x-www-form-urlencoded'}),
    withCredentials: true
  }

  httpGetOption = {
    headers: new HttpHeaders({'Content-Type': 'application/json'}),
    withCredentials: true
  }

  loginUser(loginDetails: Login): Observable<any> {
    const url =`http://localhost:5001/api/portal/auth_session/login`
    const body = new HttpParams()
    .set('email', loginDetails.email)
    .set('password', loginDetails.password)
    .set('date', "2025-02-15T12:00:00Z")
    .set("user_type", "admin")
    .set("fullName", "Moses Solomon A");
    return this.http.post<any>(url, body.toString(), this.httpGetOption)
    .pipe(
      tap((data: any) => console.log(data)),
      catchError(this.handleError<any>())
    );
  }

  currentSession(): Observable<any> {
    const url =`http://localhost:5001/api/portal/auth_session`
    return this.http.get<any>(url, this.httpGetOption)
    .pipe(
      tap((data: any) => console.log(data)),
      catchError(this.handleError<any>())
    );
  }

  // getUser(id: string): Observable<unknown> {
  //   return this.http.get<unknown>()
  // }

  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
      console.log("error message", error.statusText);
      return of(result as T);
    }
  }
}
