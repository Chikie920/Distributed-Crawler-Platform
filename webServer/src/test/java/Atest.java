import com.chikie.config.SpringConfig;
import com.chikie.service.UserService;
import org.junit.jupiter.api.Test;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

public class Atest {
    @Test
    public void atest() {
        AnnotationConfigApplicationContext springContext = new AnnotationConfigApplicationContext(SpringConfig.class);
        UserService bean = springContext.getBean(UserService.class);
        bean.checkAll().forEach(user -> System.out.println(user));
        System.out.println(bean.checkOne(1));
    }
}
