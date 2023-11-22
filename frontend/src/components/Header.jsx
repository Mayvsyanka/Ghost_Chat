import React, { useContext } from "react";
import { UserContext } from "../context/UserContext";

const Header = ({ title }) => {
  const [token, setToken] = useContext(UserContext);

  const handleLogout = () => {
    setToken(null);
  };

  const deleteUser = async () => {
    try {
      // Ваш URL для удаления пользователя
      const apiUrl = "http://127.0.0.1:8000/api/user/delete_user";

      // Заголовок с авторизацией токена
      const headers = new Headers();
      headers.append("Authorization", `Bearer ${token}`);

      // Выполнение запроса DELETE для удаления пользователя
      const response = await fetch(apiUrl, {
        method: "DELETE",
        headers: headers,
      });

      // Если запрос завершен успешно, вы можете обработать ответ по желанию
      console.log(response);

      // После успешного удаления пользователя также можно выйти из аккаунта
      setToken(null);
    } catch (error) {
      // Обработка ошибок, например, вывод в консоль
      console.error("Error deleting user:", error.message);
    }
  };

  return (
    <>
      <figure className="image is-flex is-justify-content-center">
        <img
          src="https://i.ibb.co/tp1Q4Y2/Ghostgam.jpg"
          style={{
            maxWidth: "200px",
            width: "100%",
            position: "fixed",
            top: "10px",
            left: "10px",
          }}
          alt="Logo"
        />
      </figure>
      <h1 className="title" style={{ top: "-300px" }}>
        {title}
      </h1>
      {token && (
        <>
          <button
            className="button is-danger "
                      style={{
              maxWidth: "200px",
              position: "fixed",
              top: "10px",
              right: "10px",
            }}
            onClick={handleLogout}
          >
            Logout
          </button>
          <button
            className="button is-danger "
            style={{
              position: "fixed",
              top: "10px",
              right: "100px",
            }}
            onClick={deleteUser}
          >
            Delete account
          </button>
        </>
      )}
    </>
  );
};

export default Header;