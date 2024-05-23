تسک گنجینه
===

برای انجام این پروژه ۵ روز زمان دارید و راه ارتباطی شما با ما از طریق همین ایمیل می باشد
---
نمایش و بررسی پروژه به ما به هر روشی که راحتید مشکلی نداره
---

برنامه ای بنویسید که با توجه به قیمت یک توکن در یک سال گذشته به ما بگوید در چه بازه زمانی خرید و فروش بیشترین سود را داشته است.

در این برنامه ۳ نوع کاربر داریم:

* همه کاربر ها نیاز به ثبت نام و ورود دارن
* کاربر معمولی که برای استفاده از این api  لیمیت ۱۰ کردیت در روز را دارد و فقط میتواند برای btc  از این api  اسفاده کند.
* دو نوع اشتراک داریم و هر اشتراک محدودیت هایی دارد
* هر اشتراک تعدادی کردیت میده به کاربر و بسته به نوع اشتراک زمان هم داره بعد از اتمام کردیت یا زمان یا تایید مدیر مبنی بعد افزایش کردیت یا زمان به کاربر اطلاع باید بده 
* اشتراک اول به این صورت میباشد که کاربر میاد و درخواست میده برای دسترسی به توکن های بیشتر و بعد از تایید مدیر بقیه توکن ها هم دسترسی داره ولی کردیت استفاده در روز همون لیمیت ۱۰ تا هستش
* اشتراک دوم به این صورت هستش که کاربر درخواست میده برای افزایش کردیت روزانه که اونم بعد از تایید مدیر اضافه میشه
* اشتراک دوم یه حالت دیگه هم داره که اینجوریه نیاز نیست برای افزایش لیمیتش هر روز درخواست بده درخواستش رو به صورت ماهیانه میده و بعد از تایید مدیر تا اون بازه برای این کاربر اون تعداد لیمیت در روز رو داره
* برای btc هر درخواست ۱ کردیت کم میکنه eth ۲ کردیت trx ۳ کردیت
* بارگذاری دیتای هر کدوم از توکن ها توسط ادمین انجام میشود و به صورت نمونه سه تا توکن به شما داده می شود و اگر مدیری یک فایل رو بارگذاری مجدد کرد دیتا بر اساس روز و توکن یدونه هستش
* کاربر معمولی بازه های انتخابیش ماکسیمم میتونه یک ماه باشه ولی کاربر ویژه میتونه بازه بیشتری رو انتخاب کنه
* یک api مخصوص هم داریم برای کاربر ویژه که ۱۰ کردیت مصرف میکنه که بهش بازه های پر سود رو میگه که ماکسیمم ۶ بازه پر سود توی اون بازه ای که مشخص میکنه میشه و دقیقن همین api که باز پر ضرر رو میگه

===

A project Django project .

<br>
<h2>How to Run? </h2>
<br>

<h2>
  Run with Docker
</h2>

<div class="highlight highlight-source-shell">

  ```
  $  docker build -t ganjineh_task_app_nginx . 
  ```

  <br>
  
  ```
  $   docker build -t ganjineh_task_app .
  ```

  <br>
  
  ```
  $   docker network create database_network
  ```

  <br>
  
  ```
  $   docker network create redis_bridge_monitoring

  ```
 <br>
 
  ```
  $   docker build -t ganjineh_task_app_nginx:latest -f Dockerfile.nginx .

  ```
 <br>
  
  ```
  $   docker-compose up -d
  ```

</div>

<h3>Now you can Login in http://127.0.0.1:8085/</h3>
<div class="highlight highlight-source-shell">

  ```
  $ username: admin
  ```
  <br>
  
  ```
  $ password: admin
  ```
</div>


<h2>
  Run without Docker
</h2>
<h2>
  Create a new virtual environment and activate it.
</h2>

<h3>on Windows:</h3>
<div class="highlight highlight-source-shell">

  ```
  $ pip install virtualenv
  ```
  <br>
  
  ```
  $ virtualenv your_virtualenv_name
  ```
</div>


<h3>on Linux:</h3>
<div class="highlight highlight-source-shell">

  ```
  $ sudo apt-get install python-pip
  ```
  <br>
  
  ```
  $ pip install virtualenv
  ```
  <br>
  
  ```
  $ virtualenv your_virtualenv_name
  ```
</div>

<br>

<h2>
  Set all required environment variables:
</h2>

<h3>Example on Windows:</h3>
<div class="highlight highlight-source-shell">

  ```
  $ set SECRET_KEY=abbass
  ```
</div>

<h3>Example on Linux:</h3>
<div class="highlight highlight-source-shell">

  ```
  $ export SECRET_KEY=abbass
  ```
</div>
<br>

<h2>
  Install the dependencies:
</h2>
<div class="highlight highlight-source-shell">

  ```
  $ pip install -r requirements.txt
  ```
</div>
<br>

<h2>
  Create and migrate the database:
</h2>
<div class="highlight highlight-source-shell">

  ```
  $ python manage.py migrate
  ```
</div>
<br>

<h2>
  Create a new superuser:
</h2>
<div class="highlight highlight-source-shell">

  ```
  $ python manage.py createsuperuser
  ```
</div>
<br>

<h2>
  Collect static files:
</h2>
<div class="highlight highlight-source-shell">

  ```
  $ python manage.py collectstatic
  ```
</div>
<br>

<h2>
  Run the server on default port 8000:
</h2>
<div class="highlight highlight-source-shell">

  ```
  $ python manage.py runserver
  ```
</div>
<br>

<h2>
  Start Redis Server
</h2>
<br>

<h2>
  Run celery workers and beats
</h2>
<div class="highlight highlight-source-shell">

  ```
  $ celery -A core worker --loglevel=info
  ```

  <br>

   ```
  $ celery -A core beat --loglevel=info
  ```
</div>
<br>

<h2>
  Enjoy it :)
</h2>