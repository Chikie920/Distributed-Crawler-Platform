import com.chikie.config.SpringConfig;
import com.chikie.entity.News;
import com.chikie.service.NewsService;
import org.junit.jupiter.api.Test;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

public class Atest {
    @Test
    public void atest() {
        AnnotationConfigApplicationContext springContext = new AnnotationConfigApplicationContext(SpringConfig.class);
        NewsService bean = springContext.getBean(NewsService.class);
        System.out.println(bean.getNewsById("baiduNews202402273"));
        System.out.println(bean.updateNews(new News("baiduNews202402273", "22222","2024-01-01", "22222")));
        System.out.println(bean.deleteNews("baiduNews202402273"));
    }
}
