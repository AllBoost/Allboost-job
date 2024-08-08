   <?php
   include 'db.php';

   // Проверка на наличие GET параметра 'user_id'
   if (isset($_GET['user_id'])) {
       $user_id = $_GET['user_id'];
       $conn = connect();

       // Проверка, существует ли пользователь в базе данных
       $stmt = $conn->prepare("SELECT * FROM users WHERE user_id = ?");
       $stmt->bind_param("i", $user_id);
       $stmt->execute();
       $result = $stmt->get_result();

       if ($result->num_rows == 0) {
           // Если пользователь не найден, добавляем его
           $stmt = $conn->prepare("INSERT INTO users (user_id) VALUES (?)");
           $stmt->bind_param("i", $user_id);
           $stmt->execute();
       }

       // Закрываем соединение
       $stmt->close();
       $conn->close();
       
       // Отображаем приветственную страницу
       echo '<img src="welcome.gif" alt="Welcome to AllBoost-job">';
   } else {
       echo "User ID not provided.";
   }
   ?>
   
