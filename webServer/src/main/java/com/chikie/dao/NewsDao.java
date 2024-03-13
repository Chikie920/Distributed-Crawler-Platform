package com.chikie.dao;

import com.chikie.entity.News;
import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface NewsDao {
    @Select("SELECT * FROM news LIMIT 20")
    List<News> getAllNews();

    @Select("SELECT content FROM news")
    List<String> getAllContent();

    @Select("SELECT * FROM news WHERE id = #{id}")
    News getNewsById(String id);

    @Select("SELECT * FROM news WHERE id LIKE '${taskName}%'")
    List<News> getNewsByTaskName(String taskName);

    @Select("SELECT id FROM news")
    List<String> getAllId();

    @Select("SELECT COUNT(*) FROM news WHERE id LIKE '%${time}%'")
    int getNewsCountsByTime(String time);

    @Update("UPDATE news SET title=#{title}, date=#{date}, content=#{content} WHERE id = #{id}")
    int updateNews(@Param("id") String id, @Param("title") String title, @Param("date") String date , @Param("content") String content);

    @Delete("DELETE FROM news WHERE id = #{id}")
    int deleteNews(@Param("id") String id);
}
